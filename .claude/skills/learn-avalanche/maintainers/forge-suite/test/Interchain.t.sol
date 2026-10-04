// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {
    ITeleporterMessenger,
    TeleporterMessageInput
} from "../src/ITeleporter.sol";
import {BadgeAnnouncer} from "../src/BadgeAnnouncer.sol";
import {BadgeMirror} from "../src/BadgeMirror.sol";

/// Gerçek Teleporter yerine sahte (mock) bir messenger: zincirler arası yolculuğu simüle etmeden
/// "doğru struct'ı yolluyor muyuz, alıcı yanlış göndericiyi reddediyor mu?" sorularını hızlıca test eder.
/// Gerçek uçtan uca test Fuji C-Chain ↔ kendi L1'in arasında yapılır (Stage 6 canlı kısmı).
contract MockMessenger is ITeleporterMessenger {
    bytes32 public lastDest;
    address public lastDestAddr;
    uint256 public lastGasLimit;
    bytes public lastMessage;

    function sendCrossChainMessage(TeleporterMessageInput calldata m) external returns (bytes32) {
        lastDest = m.destinationBlockchainID;
        lastDestAddr = m.destinationAddress;
        lastGasLimit = m.requiredGasLimit;
        lastMessage = m.message;
        return keccak256("msg-1");
    }
}

contract InterchainTest is Test {
    MockMessenger messenger;
    BadgeAnnouncer announcer;
    BadgeMirror mirror;

    bytes32 constant SRC = keccak256("chain-A");
    bytes32 constant DST = keccak256("chain-B");
    address alice = makeAddr("alice");
    address stranger = makeAddr("stranger");

    function setUp() public {
        messenger = new MockMessenger();
        announcer = new BadgeAnnouncer(address(messenger));
        mirror = new BadgeMirror(address(messenger), SRC, address(announcer));
    }

    function test_AnnounceBuildsCorrectMessage() public {
        bytes32 id = announcer.announce(DST, address(mirror), alice, "Workshop");
        assertEq(id, keccak256("msg-1"));
        assertEq(messenger.lastDest(), DST);
        assertEq(messenger.lastDestAddr(), address(mirror));
        assertEq(messenger.lastGasLimit(), 200_000);
        (address who, string memory name) = abi.decode(messenger.lastMessage(), (address, string));
        assertEq(who, alice);
        assertEq(name, "Workshop");
    }

    function test_RevertWhen_NonOwnerAnnounces() public {
        vm.prank(stranger);
        vm.expectRevert(BadgeAnnouncer.NotOwner.selector);
        announcer.announce(DST, address(mirror), alice, "x");
    }

    function test_MirrorAcceptsMessageFromTrustedOrigin() public {
        vm.prank(address(messenger));
        mirror.receiveTeleporterMessage(SRC, address(announcer), abi.encode(alice, "Workshop"));
        assertEq(mirror.announcedCount(alice), 1);
        assertEq(mirror.announcedAt(alice, 0), "Workshop");
    }

    function test_RevertWhen_CallerIsNotMessenger() public {
        vm.prank(stranger); // birisi doğrudan alıcıyı çağırıp sahte mesaj uyduruyor
        vm.expectRevert(BadgeMirror.NotMessenger.selector);
        mirror.receiveTeleporterMessage(SRC, address(announcer), abi.encode(alice, "Fake"));
    }

    function test_RevertWhen_OriginChainIsWrong() public {
        vm.prank(address(messenger));
        vm.expectRevert(BadgeMirror.UntrustedOrigin.selector);
        mirror.receiveTeleporterMessage(keccak256("evil-chain"), address(announcer), abi.encode(alice, "Fake"));
    }

    function test_RevertWhen_OriginSenderIsWrong() public {
        vm.prank(address(messenger));
        vm.expectRevert(BadgeMirror.UntrustedOrigin.selector);
        mirror.receiveTeleporterMessage(SRC, stranger, abi.encode(alice, "Fake"));
    }
}

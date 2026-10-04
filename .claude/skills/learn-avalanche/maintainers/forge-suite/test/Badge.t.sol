// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {IERC721} from "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import {IAccessControl} from "@openzeppelin/contracts/access/IAccessControl.sol";
import {Badge} from "../src/Badge.sol";

/// Stage 2 şartnamesi. Kontrat: src/Badge.sol (OpenZeppelin v5 ERC721 + AccessControl).
contract BadgeTest is Test {
    Badge badge;
    address admin = makeAddr("admin");
    address minter = makeAddr("minter");
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");

    function setUp() public {
        badge = new Badge(admin);
        bytes32 role = badge.MINTER_ROLE();
        vm.prank(admin);
        badge.grantRole(role, minter);
    }

    function test_MinterCanMint() public {
        vm.prank(minter);
        uint256 id = badge.mint(alice, "Workshop");
        assertEq(badge.ownerOf(id), alice);
        assertEq(badge.badgeName(id), "Workshop");
        assertEq(badge.balanceOf(alice), 1);
    }

    function test_IdsIncrement() public {
        vm.startPrank(minter);
        assertEq(badge.mint(alice, "a"), 0);
        assertEq(badge.mint(bob, "b"), 1);
        vm.stopPrank();
    }

    function test_RevertWhen_NonMinterMints() public {
        bytes32 role = badge.MINTER_ROLE();
        vm.prank(alice);
        vm.expectRevert(abi.encodeWithSelector(IAccessControl.AccessControlUnauthorizedAccount.selector, alice, role));
        badge.mint(alice, "Workshop");
    }

    function test_RevertWhen_HolderTransfers() public {
        vm.prank(minter);
        uint256 id = badge.mint(alice, "Workshop");

        vm.prank(alice);
        vm.expectRevert(Badge.Soulbound.selector);
        badge.transferFrom(alice, bob, id);
    }

    function test_RevertWhen_ApprovedOperatorTransfers() public {
        vm.prank(minter);
        uint256 id = badge.mint(alice, "Workshop");

        vm.prank(alice);
        badge.approve(bob, id);

        vm.prank(bob);
        vm.expectRevert(Badge.Soulbound.selector);
        badge.transferFrom(alice, bob, id);
    }

    function test_HolderCanBurnOwnBadge() public {
        vm.prank(minter);
        uint256 id = badge.mint(alice, "Workshop");

        vm.prank(alice);
        badge.burn(id);
        assertEq(badge.balanceOf(alice), 0);
    }

    function test_RevertWhen_StrangerBurns() public {
        vm.prank(minter);
        uint256 id = badge.mint(alice, "Workshop");

        vm.prank(bob);
        vm.expectRevert(); // ERC721InsufficientApproval
        badge.burn(id);
    }

    function test_SupportsBothInterfaces() public view {
        assertTrue(badge.supportsInterface(type(IERC721).interfaceId));
        assertTrue(badge.supportsInterface(type(IAccessControl).interfaceId));
    }
}

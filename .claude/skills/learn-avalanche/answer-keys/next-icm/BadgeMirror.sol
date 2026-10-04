// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ITeleporterReceiver} from "./ITeleporter.sol";

/// Stage 6 (alıcı taraf). Gelen mesajı KİMİN yolladığını doğrulamadan kabul eden alıcı, herkesin
/// sahte "rozet kazandı" yazabildiği bir kontrattır. Üç kontrol de şart:
///   1) çağıran gerçekten Teleporter mı?      2) mesaj beklediğimiz zincirden mi?
///   3) o zincirdeki beklediğimiz gönderici mi?
/// ANSWER KEY: ajan bunu öğrenciye VERMEZ; ipucu merdiveninin son basamağıdır.
contract BadgeMirror is ITeleporterReceiver {
    address public immutable messenger;
    bytes32 public immutable sourceChain;
    address public immutable trustedSender;

    mapping(address => string[]) private _announced;

    event BadgeMirrored(address indexed who, string name);

    error NotMessenger();
    error UntrustedOrigin();

    constructor(address messenger_, bytes32 sourceChain_, address trustedSender_) {
        messenger = messenger_;
        sourceChain = sourceChain_;
        trustedSender = trustedSender_;
    }

    function receiveTeleporterMessage(bytes32 originChainID, address originSenderAddress, bytes calldata message)
        external
    {
        if (msg.sender != messenger) revert NotMessenger();
        if (originChainID != sourceChain || originSenderAddress != trustedSender) revert UntrustedOrigin();

        (address who, string memory name) = abi.decode(message, (address, string));
        _announced[who].push(name);
        emit BadgeMirrored(who, name);
    }

    function announcedCount(address who) external view returns (uint256) {
        return _announced[who].length;
    }

    function announcedAt(address who, uint256 i) external view returns (string memory) {
        return _announced[who][i];
    }
}

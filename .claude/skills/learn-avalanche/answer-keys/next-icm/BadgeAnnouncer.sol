// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {
    ITeleporterMessenger,
    TeleporterMessageInput,
    TeleporterFeeInfo
} from "./ITeleporter.sol";

/// Stage 6 (gönderici taraf) — "bu adres şu rozeti kazandı" bilgisini başka bir Avalanche zincirine yollar.
/// ANSWER KEY: ajan bunu öğrenciye VERMEZ; ipucu merdiveninin son basamağıdır.
contract BadgeAnnouncer {
    ITeleporterMessenger public immutable messenger;
    address public immutable owner;

    event Announced(bytes32 indexed messageID, bytes32 indexed destinationChain, address who, string name);

    error NotOwner();

    constructor(address messenger_) {
        messenger = ITeleporterMessenger(messenger_);
        owner = msg.sender;
    }

    function announce(bytes32 destinationChain, address destinationMirror, address who, string calldata name)
        external
        returns (bytes32 messageID)
    {
        if (msg.sender != owner) revert NotOwner();

        messageID = messenger.sendCrossChainMessage(
            TeleporterMessageInput({
                destinationBlockchainID: destinationChain,
                destinationAddress: destinationMirror,
                feeInfo: TeleporterFeeInfo({feeTokenAddress: address(0), amount: 0}),
                requiredGasLimit: 200_000, // alıcı fonksiyonun gerçek gas'ına göre ölç, sonra ayarla
                allowedRelayerAddresses: new address[](0),
                message: abi.encode(who, name)
            })
        );
        emit Announced(messageID, destinationChain, who, name);
    }
}

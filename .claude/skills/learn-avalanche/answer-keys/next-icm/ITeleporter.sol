// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// Stage 6 — ICM (Teleporter) arayüzünün MİNİMAL yerel kopyası.
///
/// Neden yerel kopya? Öğrenci ABI'yi satır satır görsün diye. Gerçek projede
/// `ava-labs/icm-contracts` paketinden `ITeleporterMessenger` / `ITeleporterReceiver` import edilir.
/// Bu imzalar 2026-09-30'da Fuji C-Chain'deki canlı TeleporterMessenger bytecode'una karşı doğrulandı
/// (`sendCrossChainMessage` selector'ü 0x62448850 bytecode içinde bulundu). Emin değilsen tekrar doğrula:
///   cast sig "sendCrossChainMessage((bytes32,address,(address,uint256),uint256,address[],bytes))"
struct TeleporterFeeInfo {
    address feeTokenAddress; // address(0) = ücret yok
    uint256 amount;
}

struct TeleporterMessageInput {
    bytes32 destinationBlockchainID; // hedef zincirin 32-byte ID'si (chain ID DEĞİL!)
    address destinationAddress; // hedefte mesajı alacak kontrat
    TeleporterFeeInfo feeInfo;
    uint256 requiredGasLimit; // relayer'ın hedefte receive fonksiyonuna vermesi gereken gas
    address[] allowedRelayerAddresses; // boş = herhangi bir relayer
    bytes message;
}

interface ITeleporterMessenger {
    function sendCrossChainMessage(TeleporterMessageInput calldata messageInput) external returns (bytes32 messageID);
}

interface ITeleporterReceiver {
    function receiveTeleporterMessage(bytes32 originChainID, address originSenderAddress, bytes calldata message)
        external;
}

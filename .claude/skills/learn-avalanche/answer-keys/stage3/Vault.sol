// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/// Stage 3 laboratuvarı. Bu dosya KASITLI OLARAK bir açık içerir (VulnerableVault).
/// Sadece eğitim içindir — gerçek para tutan hiçbir yere kopyalama.
interface IVault {
    function deposit() external payable;
    function withdraw() external;
}

/// Açık: para gönderilir (interaction) ve bakiye ANCAK ONDAN SONRA sıfırlanır (effect).
/// Alıcı bir kontratsa `receive()` içinden withdraw()'a geri girip (re-enter) aynı bakiyeyi
/// tekrar tekrar çekebilir.
contract VulnerableVault is IVault {
    mapping(address => uint256) public balanceOf;

    function deposit() external payable {
        balanceOf[msg.sender] += msg.value;
    }

    function withdraw() external {
        uint256 amount = balanceOf[msg.sender];
        require(amount > 0, "nothing");
        (bool ok,) = msg.sender.call{value: amount}(""); // interaction
        require(ok, "send failed");
        balanceOf[msg.sender] = 0; // effect — çok geç
    }
}

/// Düzeltme 1 (asıl çözüm): Checks → Effects → Interactions sırası.
/// Düzeltme 2 (ikinci kat savunma): nonReentrant kilidi.
contract SafeVault is IVault, ReentrancyGuard {
    mapping(address => uint256) public balanceOf;

    error NothingToWithdraw();
    error TransferFailed();

    function deposit() external payable {
        balanceOf[msg.sender] += msg.value;
    }

    function withdraw() external nonReentrant {
        uint256 amount = balanceOf[msg.sender];
        if (amount == 0) revert NothingToWithdraw(); // check
        balanceOf[msg.sender] = 0; // effect
        (bool ok,) = msg.sender.call{value: amount}(""); // interaction
        if (!ok) revert TransferFailed();
    }
}

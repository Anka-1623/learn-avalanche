// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {StdInvariant} from "forge-std/StdInvariant.sol";
import {VulnerableVault, SafeVault, IVault} from "../src/Vault.sol";
import {Attacker} from "./Attacker.sol";

/// Stage 3 — saldırıyı gerçekten çalıştır, sonra düzeltmenin onu durdurduğunu kanıtla.
contract VaultReentrancyTest is Test {
    address victim = makeAddr("victim");

    function _fund(IVault v) internal {
        vm.deal(victim, 10 ether);
        vm.prank(victim);
        v.deposit{value: 10 ether}();
    }

    function test_Exploit_DrainsVulnerableVault() public {
        VulnerableVault vault = new VulnerableVault();
        _fund(vault);

        Attacker attacker = new Attacker(vault);
        attacker.attack{value: 1 ether}(); // 1 ETH'i test kontratı (address(this)) veriyor

        // 1 ETH yatırdı, 11 ETH ile çıktı: kurbanın 10 ETH'i gitti.
        assertEq(address(vault).balance, 0, "vault drained");
        assertEq(address(attacker).balance, 11 ether, "attacker took everything");
    }

    function test_Fix_SafeVaultBlocksTheSameAttack() public {
        SafeVault vault = new SafeVault();
        _fund(vault);

        Attacker attacker = new Attacker(vault);
        vm.expectRevert(); // iç içe withdraw() geri çevrilir → dış call başarısız → attack() revert
        attacker.attack{value: 1 ether}();

        assertEq(address(vault).balance, 10 ether, "victim funds intact");
        assertEq(vault.balanceOf(victim), 10 ether);
    }

    /// Fuzz: Foundry yüzlerce rastgele `amount` dener. "Yatırdığını geri alırsın" her girdide doğru mu?
    function testFuzz_DepositThenWithdrawRoundtrip(uint96 amount) public {
        vm.assume(amount > 0);
        SafeVault vault = new SafeVault();
        address user = makeAddr("user");
        vm.deal(user, amount);

        vm.startPrank(user);
        vault.deposit{value: amount}();
        vault.withdraw();
        vm.stopPrank();

        assertEq(user.balance, amount);
        assertEq(address(vault).balance, 0);
    }
}

/// Invariant testi: "ne olursa olsun bu doğru kalmalı" kuralı. Foundry `Handler`'ın fonksiyonlarını
/// rastgele sırayla, rastgele argümanlarla çağırır ve her adımdan sonra invariant'ı kontrol eder.
contract VaultHandler is Test {
    SafeVault public vault;
    uint256 public ghostDeposited;
    uint256 public ghostWithdrawn;
    address[] internal actors;

    constructor(SafeVault v) {
        vault = v;
        for (uint256 i = 0; i < 3; i++) {
            actors.push(makeAddr(string.concat("actor", vm.toString(i))));
        }
    }

    function deposit(uint256 actorSeed, uint96 amount) external {
        address a = actors[actorSeed % actors.length];
        vm.deal(a, amount);
        vm.prank(a);
        vault.deposit{value: amount}();
        ghostDeposited += amount;
    }

    function withdraw(uint256 actorSeed) external {
        address a = actors[actorSeed % actors.length];
        uint256 bal = vault.balanceOf(a);
        if (bal == 0) return;
        vm.prank(a);
        vault.withdraw();
        ghostWithdrawn += bal;
    }
}

contract VaultInvariantTest is StdInvariant, Test {
    SafeVault vault;
    VaultHandler handler;

    function setUp() public {
        vault = new SafeVault();
        handler = new VaultHandler(vault);
        targetContract(address(handler));
    }

    /// Kasadaki gerçek AVAX = yatırılan − çekilen. Bu eşitlik bozulursa para "kaybolmuş" ya da "türetilmiş" demektir.
    function invariant_VaultBalanceMatchesAccounting() public view {
        assertEq(address(vault).balance, handler.ghostDeposited() - handler.ghostWithdrawn());
    }
}

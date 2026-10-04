// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Script, console} from "forge-std/Script.sol";
import {Badge} from "../src/Badge.sol";

/// Stage 4 — Fuji'ye deploy.
///
///   BADGE_ADMIN=0xSenin_Cuzdanin forge script script/DeployBadge.s.sol \
///     --rpc-url fuji-c --account fuji-dev --sender 0xSenin_Cuzdanin --broadcast
///
/// Neden `msg.sender` yerine BADGE_ADMIN? Script içinde `msg.sender`, keystore hesabı DEĞİL,
/// Foundry'nin varsayılan script göndericisidir (--sender vermezsen). Admin'i yanlış adrese
/// verirsin ve kendi rozetini mint edemezsin. Açık env değişkeni bu tuzağı kapatır.
contract DeployBadge is Script {
    function run() external returns (Badge badge) {
        address admin = vm.envAddress("BADGE_ADMIN");

        vm.startBroadcast();
        badge = new Badge(admin);
        vm.stopBroadcast();

        console.log("Badge deployed at:", address(badge));
        console.log("Admin (DEFAULT_ADMIN_ROLE):", admin);
    }
}

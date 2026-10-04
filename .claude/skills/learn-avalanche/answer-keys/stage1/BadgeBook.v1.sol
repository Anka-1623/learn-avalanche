// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// Stage 1 / Ders 1.1 — state, struct, mapping, storage/memory/calldata.
/// ANSWER KEY: ajan bunu öğrenciye VERMEZ; ipucu merdiveninin son basamağıdır.
contract BadgeBook {
    struct Badge {
        string name;
        uint64 awardedAt;
    }

    mapping(address => Badge[]) private _badges;

    function award(address to, string calldata name) external {
        _badges[to].push(Badge({name: name, awardedAt: uint64(block.timestamp)}));
    }

    function badgeCount(address who) external view returns (uint256) {
        return _badges[who].length;
    }

    function badgesOf(address who) external view returns (Badge[] memory) {
        return _badges[who];
    }
}

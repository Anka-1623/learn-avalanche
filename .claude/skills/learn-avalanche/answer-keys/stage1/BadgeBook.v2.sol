// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// Stage 1 / Ders 1.2 — constructor, msg.sender, modifier, custom error, revert.
/// ANSWER KEY: ajan bunu öğrenciye VERMEZ; ipucu merdiveninin son basamağıdır.
contract BadgeBook {
    struct Badge {
        string name;
        uint64 awardedAt;
    }

    address public owner;
    mapping(address => Badge[]) private _badges;

    error NotOwner();
    error EmptyName();

    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function award(address to, string calldata name) external onlyOwner {
        if (bytes(name).length == 0) revert EmptyName();
        _badges[to].push(Badge({name: name, awardedAt: uint64(block.timestamp)}));
    }

    function badgeCount(address who) external view returns (uint256) {
        return _badges[who].length;
    }

    function badgesOf(address who) external view returns (Badge[] memory) {
        return _badges[who];
    }
}

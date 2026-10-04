// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// Stage 1 / Ders 1.3 — events (off-chain dünya zincirin ne olduğunu böyle duyar).
/// ANSWER KEY: ajan bunu öğrenciye VERMEZ; ipucu merdiveninin son basamağıdır.
contract BadgeBook {
    struct Badge {
        string name;
        uint64 awardedAt;
    }

    address public owner;
    mapping(address => Badge[]) private _badges;

    event BadgeAwarded(address indexed to, uint256 indexed index, string name);

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
        Badge[] storage list = _badges[to];
        list.push(Badge({name: name, awardedAt: uint64(block.timestamp)}));
        emit BadgeAwarded(to, list.length - 1, name);
    }

    function badgeCount(address who) external view returns (uint256) {
        return _badges[who].length;
    }

    function badgesOf(address who) external view returns (Badge[] memory) {
        return _badges[who];
    }
}

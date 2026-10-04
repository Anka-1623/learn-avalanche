// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {BadgeBook} from "../src/BadgeBook.sol";

/// Ders 1.1 — state, struct, mapping. Test dosyası = şartname; kontratı sen yazıyorsun.
contract BadgeBookTest is Test {
    BadgeBook book;
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");

    function setUp() public {
        book = new BadgeBook();
    }

    function test_NewAddressHasNoBadges() public view {
        assertEq(book.badgeCount(alice), 0);
    }

    function test_AwardStoresNameAndTimestamp() public {
        vm.warp(1_700_000_000);
        book.award(alice, "Workshop");

        BadgeBook.Badge[] memory list = book.badgesOf(alice);
        assertEq(list.length, 1);
        assertEq(list[0].name, "Workshop");
        assertEq(list[0].awardedAt, 1_700_000_000);
    }

    function test_CountGrowsWithEachAward() public {
        book.award(alice, "Workshop");
        book.award(alice, "Hackathon");
        assertEq(book.badgeCount(alice), 2);
        assertEq(book.badgesOf(alice)[1].name, "Hackathon");
    }

    function test_BadgesAreSeparatePerAddress() public {
        book.award(alice, "Workshop");
        assertEq(book.badgeCount(alice), 1);
        assertEq(book.badgeCount(bob), 0);
    }
}

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {BadgeBook} from "../src/BadgeBook.sol";

/// Ders 1.3 — L2 testlerinin hepsi + event. `test/BadgeBook.t.sol` ÜZERİNE YAZILIR.
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

    function test_OwnerIsDeployer() public view {
        assertEq(book.owner(), address(this));
    }

    function test_RevertWhen_NonOwnerAwards() public {
        vm.prank(alice);
        vm.expectRevert(BadgeBook.NotOwner.selector);
        book.award(bob, "Workshop");
    }

    function test_RevertWhen_NameIsEmpty() public {
        vm.expectRevert(BadgeBook.EmptyName.selector);
        book.award(alice, "");
    }

    // --- yeni: event ---

    function test_AwardEmitsEventWithIndex() public {
        // (topic1: to, topic2: index, topic3 yok, data: name)
        vm.expectEmit(true, true, false, true, address(book));
        emit BadgeBook.BadgeAwarded(alice, 0, "Workshop");
        book.award(alice, "Workshop");

        vm.expectEmit(true, true, false, true, address(book));
        emit BadgeBook.BadgeAwarded(alice, 1, "Hackathon");
        book.award(alice, "Hackathon");
    }
}

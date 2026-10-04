// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";

/// Stage 2 — miras, standart (ERC-721), rol tabanlı erişim, "soulbound" (devredilemez) rozet.
/// ANSWER KEY: ajan bunu öğrenciye VERMEZ; ipucu merdiveninin son basamağıdır.
///
/// OpenZeppelin v5 notu: v4'teki `_beforeTokenTransfer` kalktı; tüm mint/transfer/burn
/// akışı tek bir `_update` fonksiyonundan geçiyor. Soulbound = `_update`'i override etmek.
contract Badge is ERC721, AccessControl {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    error Soulbound();

    uint256 private _nextId;
    mapping(uint256 id => string) public badgeName;

    constructor(address admin) ERC721("Community Badge", "BADGE") {
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
    }

    function mint(address to, string calldata name) external onlyRole(MINTER_ROLE) returns (uint256 id) {
        id = _nextId++;
        badgeName[id] = name;
        _safeMint(to, id);
    }

    /// Sahibi kendi rozetini yakabilir (mint: from==0, burn: to==0 serbest; transfer yasak).
    function burn(uint256 id) external {
        _update(address(0), id, _msgSender());
    }

    function _update(address to, uint256 tokenId, address auth) internal override returns (address) {
        address from = _ownerOf(tokenId);
        if (from != address(0) && to != address(0)) revert Soulbound();
        return super._update(to, tokenId, auth);
    }

    // ERC721 ve AccessControl ikisi de supportsInterface tanımlıyor → çakışmayı biz çözmeliyiz.
    function supportsInterface(bytes4 interfaceId) public view override(ERC721, AccessControl) returns (bool) {
        return super.supportsInterface(interfaceId);
    }
}

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

contract CopyrightRegistry {

    struct Work{
        string hash;
        address owner;
        uint timestamp;
    }

    mapping(string => Work) public works;

    function registerWork(string memory _hash) public {
        require(works[_hash].timestamp == 0, "Already registered");
        works[_hash] = Work({
            hash: _hash,
            owner: msg.sender,
            timestamp: block.timestamp
        });
    }

    function verifyWork(string memory _hash) public view returns (
        address owner,
        uint timestamp
    ) {
        require(works[_hash].timestamp != 0, "Not registered");

        Work memory w = works[_hash];
        return (w.owner, w.timestamp);
    }
}
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

contract SimpleStorage {

    // data types
    // syntax of: type visibility name
    uint256 favouriteNumber;
    // bool is_favourite = true;
    // string favouriteString = "String";
    // address favouriteAddress = 0xf0a8e667aee40BEAAcFB080029FeD978AcEaC644;
    // bytes32 favouriteBytes = "cat";

    // structs
    struct People {
        uint256 favouriteNumber;
        string name;
    }

    // an array of people
    People[] public people;

    // mapping
    mapping(string => uint256) public nameToFavouriteNumber;

    // function
    function store(uint256 _favouriteNumber) public returns(uint256){
        favouriteNumber = _favouriteNumber;
        return favouriteNumber;
    }

    // view, pure - functions that doesnt change the state so they dont require transactions
    function retrieve() public view returns(uint256) {
        return favouriteNumber;
    }

    // memory - store only on execution
    // storage - store data in persistence
    function addPerson(string memory _name, uint256 _favouriteNumber) public {
        people.push(People(_favouriteNumber, _name));
        nameToFavouriteNumber[_name] = _favouriteNumber;
    }
}
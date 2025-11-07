// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VotingSystem {
    address public admin;

    struct User {
        bool registered;
        bool voted;
    }

    struct Contestant {
        string name;
        uint voteCount;
    }

    mapping(address => User) public users;
    mapping(uint => Contestant) public contestants;
    uint public contestantCount;

    event UserRegistered(address user);
    event ContestantAdded(uint id, string name);
    event VoteCast(address voter, uint contestantId);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    function registerUser(address _user) public onlyAdmin {
        require(!users[_user].registered, "User already registered");
        users[_user] = User(true, false);
        emit UserRegistered(_user);
    }

    function addContestant(string memory _name) public onlyAdmin {
        contestants[contestantCount] = Contestant(_name, 0);
        emit ContestantAdded(contestantCount, _name);
        contestantCount++;
    }

    function vote(uint _contestantId) public {
        require(users[msg.sender].registered, "User not registered");
        require(!users[msg.sender].voted, "User has already voted");
        require(_contestantId < contestantCount, "Invalid contestant");
        users[msg.sender].voted = true;
        contestants[_contestantId].voteCount++;
        emit VoteCast(msg.sender, _contestantId);
    }

    function getContestant(uint _id) public view returns (string memory, uint) {
        Contestant memory c = contestants[_id];
        return (c.name, c.voteCount);
    }
}
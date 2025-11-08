// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract KYC {

    struct User {
        string name;
        uint age;
        string email;
        string aadhar;
        bool isRegistered;
    }

    mapping(address => User) public users;

    event UserRegistered(address user, string name);

    function registerUser(
        string memory _name,
        uint _age,
        string memory _email,
        string memory _aadhar
    ) public {
        require(!users[msg.sender].isRegistered, "Already registered");

        users[msg.sender] = User(_name, _age, _email, _aadhar, true);
        emit UserRegistered(msg.sender, _name);
    }

    function getUser(address user)
        public
        view
        returns (string memory, uint, string memory, string memory, bool)
    {
        User memory u = users[user];
        return (u.name, u.age, u.email, u.aadhar, u.isRegistered);
    }
}

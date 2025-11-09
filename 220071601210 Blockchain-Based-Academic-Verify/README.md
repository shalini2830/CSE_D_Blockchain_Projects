



A decentralized platform for managing and verifying academic and professional credentials with trust and transparency.

submitted by
sadiq ali(220071601210)
seyed mazeen(220071601227)
shaahir(220071601228)
shaheed(220071601229)



About The Project

Traditional systems for managing academic and professional records are centralized, inefficient, and vulnerable to fraud. Verifying credentials can be a slow and costly process, while diploma counterfeiting remains a significant issue.

This project introduces a decentralized application (DApp) that leverages the Ethereum blockchain to create a secure, immutable, and transparent ecosystem for credential management. By using smart contracts, the platform eliminates the need for trusted intermediaries, empowering individuals with direct ownership of their verified achievements and allowing employers or institutions to verify records instantly.

The system is designed to serve as a single source of truth for a person's entire professional journey, from academic degrees and certifications to skills and work experience.


Key Features

Decentralized Identity: Each user (individual or organization) is identified by their unique Ethereum address.

Immutable Records: Once a credential is endorsed and recorded on the blockchain, it cannot be altered or deleted.

Role-Based Access Control: The system defines three distinct roles:

Admin: Manages user registration and maintains the system.

Employee (Individual): Creates and manages their digital portfolio.

Organization Endorser: Verifies and endorses credentials (e.g., universities, companies).

Comprehensive Digital Portfolio: Individuals can add their education history, work experience, skills, and certifications.

On-Chain Endorsement System: Organizations can cryptographically sign and approve credentials, creating a verifiable link between the individual and the institution.

Real-time Notifications & Chat: A messaging system allows for communication between users, such as endorsement requests (powered by Firebase).


Technology Stack

The project is built with a modern technology stack for decentralized application development:

Frontend:

React.js: A JavaScript library for building user interfaces.

Semantic UI React: A component framework for a clean and responsive design.

Web3.js: To interact with the Ethereum blockchain.

React Router: For client-side routing.

Chart.js: For data visualization and graphs.

Backend (Blockchain):

Solidity: The programming language for writing smart contracts.

Truffle Suite: A development environment, testing framework, and asset pipeline for smart contracts.

Ganache: A personal blockchain for local development and testing.

Middleware & Services:

MetaMask: A browser extension wallet to manage accounts and sign transactions.

Firebase (Firestore): For off-chain data management, primarily for the chat and notification system.

Getting Started

Follow these instructions to set up and run a local instance of the project.

Prerequisites

Ensure you have the following software installed on your system:

Node.js (v16 or later): Download Here

Truffle Suite: npm install -g truffle

Ganache UI: Download Here

MetaMask Extension: Install for your browser

Installation & Setup

Clone the Repository

code
Sh
download
content_copy
expand_less
git clone https://github.com/ASSA2004/Block-Chain-Based-Academic-verify-main.git
cd Academic-verify-main

Install NPM Packages

code
Sh
download
content_copy
expand_less
npm install

Note: This project uses older versions of some libraries. If you encounter issues, you may need to install react-router-dom@5.2.0 and firebase@8.10.0 specifically.

Set Up the Local Blockchain

Launch the Ganache application.

Keep the default "Quickstart" workspace running. It provides the RPC server at http://127.0.0.1:7545.

Compile and Deploy Smart Contracts

Open your terminal in the project root.

Compile the contracts:

code
Sh
download
content_copy
expand_less
truffle compile

Deploy the contracts to your local Ganache network:

code
Sh
download
content_copy
expand_less
truffle migrate --reset

Configure MetaMask

Open MetaMask and add a new network with the following details:

Network Name: Ganache

RPC URL: http://127.0.0.1:7545

Chain ID: 1337 (or the ID shown in your Ganache instance)

Import an account from Ganache using its private key. The first account in Ganache is the Admin by default.

Run the React Application

code
Sh
download
content_copy
expand_less
npm start

The application will open in your browser at http://localhost:3000. Connect MetaMask when prompted.

How It Works

Registration: The Admin registers new users (both Individuals and Organizations) by adding their Ethereum addresses to the main Admin smart contract.

Profile Creation: An Individual logs in with their MetaMask account, and can start building their profile by adding their education, skills, work experience, etc. These are saved as pending entries.

Endorsement Request: The Individual sends an endorsement request to the relevant Organization for a specific credential (e.g., a university degree).

Verification & Endorsement: The Organization logs in, reviews the request, and—if valid—endorses it. This action calls a function on the smart contract, creating an immutable, on-chain record that validates the credential.

Public Verification: Anyone can now view the Individual's profile and see the verified credentials, which are cryptographically secured by the endorsing organization's signature.

Future Scope

Mobile Application: Develop a mobile app for verifiers to scan a QR code from a student's profile for instant verification.

Interoperability: Implement decentralized identity (DID) and verifiable credential (VC) standards to make the system compatible with other identity platforms.

AI-Powered Recommendations: Integrate AI to analyze verified skills and suggest personalized career paths or further learning opportunities.

Direct University Integration: Create APIs for universities to directly issue and endorse degrees on the blockchain upon graduation, streamlining the process.

License

Distributed under the MIT License. See LICENSE for more information.

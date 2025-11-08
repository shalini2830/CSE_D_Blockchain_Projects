import web3 from "./ethereum";
import KYC from "./abis/KYC.json";

let instance;

async function loadContract() {
  const networkId = await web3.eth.net.getId();
  const deployed = KYC.networks[networkId];

  if (!deployed) {
    alert("Smart contract not deployed on this network!");
    return null;
  }

  instance = new web3.eth.Contract(KYC.abi, deployed.address);
  return instance;
}

export default loadContract;

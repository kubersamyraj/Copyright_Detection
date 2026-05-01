const CopyrightRegistry = artifacts.require("copyrightRegistry");

module.exports = function (deployer) {
    deployer.deploy(CopyrightRegistry);
};
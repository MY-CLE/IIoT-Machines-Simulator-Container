"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Header = void 0;
const react_1 = __importDefault(require("react"));
require("../src/css/header.css");
const iconLogin_1 = __importDefault(require("./icons/iconLogin"));
const iconSettings_1 = __importDefault(require("./icons/iconSettings"));
function Header() {
    return (react_1.default.createElement("header", { className: "header" },
        react_1.default.createElement("h1", null, "Lasercutter HMI"),
        react_1.default.createElement("div", { className: "save" }),
        react_1.default.createElement("div", { className: "config" }),
        react_1.default.createElement("div", { className: "login" })));
}
exports.Header = Header;
exports.default = Header;

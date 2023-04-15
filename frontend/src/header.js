"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Header = void 0;
const react_1 = __importDefault(require("react"));
require("../src/css/header.css");
function Header() {
    return (react_1.default.createElement("header", { className: "header" },
        react_1.default.createElement("h1", null, "Lasercutter HMI"),
        react_1.default.createElement("div", { className: "settings" }),
        react_1.default.createElement("div", { className: "login" })));
}
exports.Header = Header;
exports.default = Header;

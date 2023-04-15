"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importDefault(require("react"));
require("../src/css/App.css");
const header_1 = __importDefault(require("./header"));
const statusBar_1 = __importDefault(require("./statusbar/statusBar"));
function App() {
    return (react_1.default.createElement("div", { className: "App" },
        react_1.default.createElement(header_1.default, null),
        react_1.default.createElement(statusBar_1.default, null)));
}
exports.default = App;

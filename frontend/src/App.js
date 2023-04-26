"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importDefault(require("react"));
require("../src/css/App.css");
require("../src/css/button.css");
const header_1 = __importDefault(require("./header"));
const statusBar_1 = __importDefault(require("./statusbar/statusBar"));
function App() {
    return (react_1.default.createElement("div", { className: "App" },
        react_1.default.createElement(header_1.default, null),
        react_1.default.createElement("div", { className: "buttoncontainer" },
            react_1.default.createElement("button", { className: "button" }, "Simulation starten"),
            react_1.default.createElement("button", { className: "button" }, "Simulation laden"))));
}
exports.default = App;

"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = __importDefault(require("react"));
require("../src/css/App.css");
const header_1 = __importDefault(require("./header"));
function App() {
    /*
    let [time, setTime] = useState([]);
  
    useEffect(() => {
      fetchTime();
    }, []);
  
    const fetchTime = () => {
      // Where we're fetching data from
      return (
        fetch("/api/time")
          // We get the API response and receive data in JSON format
          .then((response) => response.json())
          .then((data) => setTime(data.time))
          .catch((error) => console.error(error))
      );
    };
    */
    return (react_1.default.createElement("div", { className: "App" },
        react_1.default.createElement(header_1.default, null)));
}
exports.default = App;

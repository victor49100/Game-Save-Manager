import {useState} from "react";

function App() {

    //variables
    const [save, setSave] = useState();

    return (
        <>
            <h1>Game Saves</h1>
            <form>
                <select>
                    <option value="none">
                        choose a Game save
                    </option>
                </select>
                <button>Load a save</button>
            </form>
            <form>
                <select>
                    <option value="none">
                        choose a Game save
                    </option>
                </select>
                <button>Upload a save</button>
            </form>
            <form>
                <label htmlFor="">new game</label>
                <button>save path</button>
                <input type="text" />
                <button>add new games</button>
            </form>

        </>
    )
}

export default App

import { useEffect, useContext } from "react";
import { ProtectedContext } from "../../../Context/ProtectedContext.jsx";


function Logout() {
    const { setLogoutClicked } = useContext(ProtectedContext)

    return (
        <>
            <h1>Logout</h1>
            <button onClick={() => setLogoutClicked(false)}>Cancel</button>
        </>
    )
}


export default Logout

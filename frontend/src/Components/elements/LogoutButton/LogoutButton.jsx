import { useEffect, useContext } from "react";
import { ProtectedContext } from "../../../Context/ProtectedContext.jsx";

function LogoutButton() {
    const { setLogoutClicked } = useContext(ProtectedContext)

    return (
        <>
            <button onClick={() => setLogoutClicked(true)}>Logout button</button>
        </>
    )
}


export default LogoutButton

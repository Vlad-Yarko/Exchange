import { Outlet } from "react-router-dom";
import { ProtectedContextProvider } from "../../../Context/ProtectedContext.jsx";


function ProtectedMiddleware() {


    return (
        <>
            <ProtectedContextProvider>
                <Outlet />
            </ProtectedContextProvider>
        </>
    )
}


export default ProtectedMiddleware

import { Outlet } from "react-router-dom";
import { AuthFormContextProvider } from "../../Context/AuthFormContext.jsx";


function AuthFormMiddleware() {

    return (
        <AuthFormContextProvider>
            <Outlet />
        </AuthFormContextProvider>
    )
}


export default AuthFormMiddleware

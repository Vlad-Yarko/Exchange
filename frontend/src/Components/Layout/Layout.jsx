import { Outlet } from "react-router-dom";
import Header from "../Header/Header.jsx";
import Footer from "../Footer/Footer.jsx";

import { AuthContextProvider } from "../../Context/AuthContext.jsx";


function Layout() {

    return (
        <>
            <Header />
            <AuthContextProvider>
                <Outlet />
            </AuthContextProvider>
            <Footer />
        </>
    )
}

export default Layout
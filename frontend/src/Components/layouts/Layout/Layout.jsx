import { Outlet } from "react-router-dom";
import Header from "../../elements/Header/Header.jsx";
import Footer from "../../elements/Footer/Footer.jsx";
import { BaseContextProvider } from "../../../Context/BaseContext.jsx";


function Layout() {

    return (
        <>
            <BaseContextProvider>
                <Header />
                <Outlet />
                <Footer />
            </BaseContextProvider>
        </>
    )
}

export default Layout
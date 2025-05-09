import {
    createRoutesFromElements,
    createBrowserRouter,
    Route
} from "react-router-dom";
import Layout from "./Components/layouts/Layout/Layout.jsx";
import ProtectedMiddleware from "./Components/middlewares/ProtectedMiddleware/ProtectedMiddleware.jsx";
import AuthMiddleware from "./Components/middlewares/AuthMiddleware/AuthMiddleware.jsx";
import Home from "./Components/pages/Home/Home.jsx";
import Error404 from "./Components/pages/Error404/Error404.jsx";
import Signup from "./Components/pages/Singup/Signup.jsx";
import Login from "./Components/pages/Login/Login.jsx";
import Account from "./Components/pages/Account/Account.jsx";
import AuthFormMiddleware from "./Components/middlewares/AuthFormMiddleware/AuthFormMiddleware.jsx";


const router = createBrowserRouter(
    createRoutesFromElements(
        <Route path='/' element={<Layout />}>
            <Route path='' element={<ProtectedMiddleware />}>
                <Route path='' element={<Home />}/>
                <Route path='account/me' element={<Account />}/>
            </Route>
            <Route path='auth/' element={<AuthMiddleware />}>
                <Route path='' element={<AuthFormMiddleware />}>
                    <Route path='signup' element={<Signup />}/>
                    <Route path='login' element={<Login />}/>
                </Route>
            </Route>
            <Route path='*' element={<Error404 />}/>
        </Route>
    )
)


export default router

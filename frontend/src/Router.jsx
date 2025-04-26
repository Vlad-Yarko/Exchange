import {
    createRoutesFromElements,
    createBrowserRouter,
    Route
} from "react-router-dom";
import Layout from "./Components/Layout/Layout.jsx";
import Home from "./Components/Home/Home.jsx";
import Login from "./Components/Login/Login.jsx";
import Logout from "./Components/Logout/Logout.jsx";
import Signup from "./Components/Signup/Signup.jsx";
import AuthFormMiddleware from "./Components/AuthFormMiddleware/AuthFormMiddleware.jsx";
import Error404 from "./Components/Error404/Error404.jsx";
import Profile from "./Components/Profile/Profile.jsx";


const router = createBrowserRouter(
    createRoutesFromElements(
        <Route path='/' element={<Layout />}>
            <Route path='' element={<Home />}/>
            <Route path='logout' element={<Logout />}/>
            <Route path='' element={<AuthFormMiddleware />}>
                <Route path='login' element={<Login />}/>
                <Route path='signup' element={<Signup />}/>
            </Route>
            <Route path='me' element={<Profile />}/>
            <Route path='*' element={<Error404 />}/>
        </Route>
    )
)


export default router

import {useEffect, useContext, useActionState} from "react";
import { BaseContext } from "../../../Context/BaseContext.jsx";
import { ProtectedContext } from "../../../Context/ProtectedContext.jsx";
import api from "../../../api.js";
import Logout from "../../elements/Logout/Logout.jsx";
import LogoutButton from "../../elements/LogoutButton/LogoutButton.jsx";


function Account() {
    const { bearer } = useContext(BaseContext)
    const { username, email, setUsername, setEmail, logoutClicked } = useContext(ProtectedContext)


    useEffect(() => {
        document.title = 'E account'
        const fetchUserInfo = async() => {
            const response = await api.get('/account/info', {
                withCredentials: true,
                headers: {
                    'Authorization': `Bearer ${bearer}`
                }
            })
            const data = response.data
            setUsername(data.username)
            setEmail(data.email)
        }
        fetchUserInfo()
    }, [])

    return (
        <>
            <h1>Account</h1>
            <h1>Username: {username}</h1>
            <h1>Email: {email}</h1>
            {logoutClicked
                ? <Logout />
                : <LogoutButton />
            }
        </>
    )
}


export default Account

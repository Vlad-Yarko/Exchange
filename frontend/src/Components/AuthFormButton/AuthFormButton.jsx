import {Link} from "react-router-dom";

function AuthFormButton({ to, label }) {

    return (
        <h1>Don't have an account? {<Link className='text-green-500' to={to}>{label}</Link>}</h1>
    )
}


export default AuthFormButton

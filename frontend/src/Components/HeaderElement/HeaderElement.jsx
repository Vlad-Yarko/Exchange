import { useContext, useEffect } from "react";
import { NavLink, useLocation } from "react-router-dom";

import { HeaderContext } from "../../Context/HeaderContext.jsx";

function HeaderElement({ link, label }) {
    const location = useLocation()
    const { tab, setTab } = useContext(HeaderContext)

    return (
        <>
            <li className={`cursor-pointer border-2 p-2.5 rounded-full border-amber-700 
                    ${tab === link ? 'bg-amber-50' : 'bg-violet-200'}`}>
                <NavLink to={link}>{label}</NavLink>
            </li>
        </>
    )
}


export default HeaderElement

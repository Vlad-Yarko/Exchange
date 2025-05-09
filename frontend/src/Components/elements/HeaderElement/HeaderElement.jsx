import { useContext, useEffect } from "react";
import { NavLink, useLocation } from "react-router-dom";
import { BaseContext } from "../../../Context/BaseContext.jsx";


function HeaderElement({ link, label, links }) {
    const { tab } = useContext(BaseContext)

    return (
        <>
            <li className={`cursor-pointer border-2 p-2.5 rounded-full border-amber-700 
                    ${links.includes(tab) ? 'bg-amber-50' : 'bg-violet-200'}`}>
                <NavLink to={link}>{label}</NavLink>
            </li>
        </>
    )
}


export default HeaderElement

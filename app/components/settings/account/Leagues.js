import Button from "@mui/material/Button";
import Link from "next/link";

export default function Leagues ( u, leagues ) {

    if (!u){
        console.log("u is undifined: " + u)
        return (<p>Error: User is undefined</p>);
    }
    const user = u['user']

    return (
        <p>Leagues</p>
        
    );
}
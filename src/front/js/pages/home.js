import React, { useContext } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.css";

export const Home = () => {
	const { store, actions } = useContext(Context);

	return (
		<div className="text-center mt-5">
			<h1>Quill Project</h1>
			<h6>Made By Dylan Shafe</h6>
			
		</div>
	);
};

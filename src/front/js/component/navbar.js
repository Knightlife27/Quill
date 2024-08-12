import React from "react";
import { Link } from "react-router-dom";

export const Navbar = () => {
	return (
		<nav className="navbar navbar-light bg-light">
			<div className="container">
				<Link to="/">
					<span className="navbar-brand mb-0 h1">Quill</span>
				</Link>
				<div className="ml-auto">
					<Link to="/dashboard" className="btn btn-success">
						Dashboard
					</Link>
				</div>
			</div>
		</nav>
	);
}



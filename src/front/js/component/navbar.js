import React from "react";
import { Link } from "react-router-dom";

export const Navbar = () => {
	return (
		<nav className="navbar navbar-light bg-light">
			<div className="container">
				<Link to="/">
					<span className="navbar-brand mb-0 h1">Quill Dashboard</span>
				</Link>
				<div className="ml-auto">
					<Link to="/demo" className="btn btn-primary me-2">
						Check the Context in action
					</Link>
					<Link to="/dashboard" className="btn btn-success">
						Dashboard
					</Link>
				</div>
			</div>
		</nav>
	);
}
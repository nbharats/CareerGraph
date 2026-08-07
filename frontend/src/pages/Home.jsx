import { useEffect, useState } from "react";
import api from "../services/api";
import axios from "axios";

function Home() {

    const [jobs, setJobs] = useState([]);
    const [student, setStudent] = useState({

            name: "",
            skills: [],
            learning: []
        });

    useEffect(() => {

        axios
            .get("http://127.0.0.1:5000/recommend/Bharat")
            .then((response) => {
                setJobs(response.data);
            })
            .catch((error) => {
                console.log(error);
            });
        
        axios
        .get("http://127.0.0.1:5000/student/Bharat")
        .then((res)=>{
            setStudent(res.data);
        });

    }, []);

    return (

        <div className="container py-5">

            <div className="text-center mb-5">

                <h1 className="display-3 fw-bold">
                    CareerGraph AI
                </h1>

                <p className="lead text-secondary">
                    Graph-powered Career Recommendation System using
                    Flask, React and CognoDB
                </p>

            </div>

            {/* Student Profile */}

            <div className="card shadow-sm mb-5">

                <div className="card-body">

                    <h3>
                        <i className="fas fa-user me-2 text-primary"></i>
                        {student.name}
                    </h3>

                    <p className="text-muted">
                        Computer Science Graduate
                    </p>

                    <hr className="my-4" />

                    <h5>
                        <i className="fas fa-check-circle text-success me-2"></i>
                        Current Skills
                    </h5>

                    <div className="mb-4">

                        {student.skills.length > 0 ? (

                            student.skills.map((skill, index) => (

                                <span
                                    key={index}
                                    className="badge bg-success me-2 mb-2 fs-6"
                                >
                                    {skill}
                                </span>

                            ))

                        ) : (

                            <p>No skills found</p>

                        )}

                    </div>

                    <h5>
                        <i className="fas fa-book-open text-warning me-2"></i>
                        Currently Learning
                    </h5>

                    <div>

                        {student.learning.length > 0 ? (

                            student.learning.map((skill, index) => (

                                <span
                                    key={index}
                                    className="badge bg-warning text-dark me-2 mb-2 fs-6"
                                >
                                    {skill}
                                </span>

                            ))

                        ) : (

                            <p>Not learning any skills</p>

                        )}

                    </div>

                </div>

            </div>

            <h2 className="mb-4">
                Job Recommendations
            </h2>

            {jobs.map((job, index) => (

                <div key={index} className="card shadow-sm h-100 m-5">

                    <div className="card-body p-5">

                        <h4 className="card-title text-primary">
                            <i className="fas fa-briefcase me-2"></i>
                            {job.job}
                        </h4>

                        <h6 className="text-secondary mb-4">
                            <i className="fas fa-building me-2"></i>
                            {job.company}
                        </h6>

                        <div className="mb-4">

                            <div className="d-flex justify-content-between">

                                <strong>Match Score</strong>

                                <strong className="text-success">
                                    {job.matchScore}%
                                </strong>

                            </div>

                            <div className="progress mt-2">

                                <div
                                    className="progress-bar bg-success"
                                    role="progressbar"
                                    style={{ width: `${job.matchScore}%` }}
                                >
                                    {job.matchScore}%
                                </div>

                            </div>

                        </div>

                        <hr className="my-4" />

                        <h5>
                            <i className="fas fa-check-circle text-success me-2 mb-3"></i>
                            Matched Skills
                        </h5>

                        {
                            job.matchedSkills.length > 0 ?

                            job.matchedSkills.map((skill,index)=>(
                                <span
                                    key={index}
                                    className="badge bg-success me-2 mb-2"
                                >
                                    {skill}
                                </span>
                            ))

                            :

                            <p className="text-muted">
                                No matching skills
                            </p>
                        }

                        <hr className="my-4" />

                        <h5>
                            <i className="fas fa-times-circle text-danger me-2 mb-3"></i>
                            Missing Skills
                        </h5>

                        {
                            job.missingSkills.length > 0 ?

                            job.missingSkills.map((skill,index)=>(
                                <span
                                    key={index}
                                    className="badge bg-danger me-2 mb-2"
                                >
                                    {skill}
                                </span>
                            ))

                            :

                            <span className="badge bg-success">
                                <i className="fas fa-check me-1"></i>
                                No Missing Skills
                            </span>
                        }

                    </div>

                </div>

            ))}

        </div>

    );

}

export default Home;

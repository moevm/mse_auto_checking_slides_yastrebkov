db.createUser(
        {
            user: "flaskuser",
            pwd: "mongo_password",
            roles: [
                {
                    role: "readWrite",
                    db: "flaskdb"
                }
            ]
        }
);
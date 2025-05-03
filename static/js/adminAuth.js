let container = document.getElementById('container');
        let actionUrl = ""; // Store the action URL to redirect after authentication

        function openModal(url) {
            actionUrl = url;
            document.getElementById("adminModal").style.display = "block";
            document.getElementById("container").style.filter = "blur(5px)";
        }

        function closeModal() {
            document.getElementById("adminModal").style.display = "none";
            document.getElementById("container").style.filter = "blur(0px)";
        }

        function verifyAdmin() {
            let adminUser = document.getElementById("adminUsername").value;
            let adminPass = document.getElementById("adminPassword").value;

            if (adminUser === "UserName" && adminPass === "YourPassword") {
                // update/ change "Username" and also change "YourPassword" to your actual passWord or you can also change with your database(ex-mySQL)
                window.location.href = actionUrl;
            } else {
                alert("❌ Authentication Failed!");
            }
        }
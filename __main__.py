import connexion

# Create a swagger app with specification in ./
app = connexion.App(__name__, specification_dir="./")

# Add API from swagger yaml file definition.
# Resource routes (and therefore handler locations) are defined in the swagger 
# file.
app.add_api("swagger.yml")

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)

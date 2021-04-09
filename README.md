# 003_DispatchLite

This repository will be used to mock the requests we would be making to Dispatch. Dispatch is the universities in house application that is used to send mass amounts of
emails through dynamic templates. We will only be mocking the components we need the more specifically the requests we would be making with those components. Primarily this
involves `POST` and 'GET` requests. Because no view are associated with this repository for a client to interact with, we can use the Django Rest Framework to handle all of 
our RESTful APIs we plan to make to this code base. If a developer needs to see any particular object stored in the database, they can use the Django's Admin portal to view each 
of them.

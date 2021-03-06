var app = angular.module("blogApp", ["ngRoute"]);

app.config(function ($routeProvider) {
    $routeProvider
    .when("/", {
        templateUrl: "post_list.html",
        controller: 'PostListController'
    })
    .when("/show_post/:post_id", {
        templateUrl: "show_post.html",
        controller: "ShowPostController"
    })
    .when("/add", {
        templateUrl: "create_post.html",
        controller: "CreatePostController"
        //templateUrl: "show_post.html",
        //controller: "ShowPostController"
    })
    .otherwise({
        redirectTo: '/'
    });
});

app.controller("PostListController", function ($scope, $http) {
    console.log("Get List:Start");
    $http.get("http://localhost:5000/api/v1.0/posts")
    .then(function (response) {
        console.log("Get List:Succuess");
        $scope.posts = response.data.posts;
        //console.log(response);
    });
});

app.controller("ShowPostController", function ($scope, $http, $routeParams) {
    post_id = $routeParams.post_id;
    rest_url = "http://localhost:5000/api/v1.0/posts/" + post_id;
    $http.get(rest_url)
    .then(function (response) {
        $scope.post = response.data.post;
        console.log(response);
    });
});

app.controller("CreatePostController", function ($scope, $http, $window) {
    console.log("CreatePostController");

    // create a blank object to handle form data.
    $scope.post = {};
    // calling our submit function.
    $scope.submitForm = function () {
        // Posting data to php file
        $http({
            method: 'POST',
            url: "http://localhost:5000/api/v1.0/posts/",
            data: $scope.post,
            headers: { 'Content-Type': 'application/json' }
        })
          .success(function (data) {
              if (data.errors) {
                  // Showing errors.
                  $scope.errorName = data.errors.name;
                  $scope.errorUserName = data.errors.username;
                  $scope.errorEmail = data.errors.email;
              } else {
                  $scope.message = data.message;
              }
              $window.location.href = '/';
          });
    };
});

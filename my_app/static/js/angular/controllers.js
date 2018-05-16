
todoCtrl = Todo_app.controller('todoCtrl', function ($window, $scope, EndpointService) {
    /*********************************/
    //Methods for the integration between Angular and Endpoints

    $window.init = function() {
      $scope.$apply($scope.load_todo_api);
    };

    $scope.load_apis = function() {
        EndpointService.loadService('solicitudesApis', 'v1');
    };

    $scope.$watch(EndpointService.isLoaded, function(loaded) {
        $scope.loaded = loaded;
        if (loaded){
            console.log("Apis Loaded");
        }
    });

    /**
     * overrides window init method for notifying to graphical interface when the api was loaded

    /*************************************/
    $scope.form = {};

    $scope.info = false;
    $scope.success = false;
    $scope.danger = false;

    $scope.message = "";

    $scope.twostep = false;
    $scope.tree_step = false;
    $scope.last_step = false;

    $scope.clearData = function(){
        $scope.form = {};
        $scope.twostep = false ;
        $scope.tree_step = false;

        $scope.clearAlerts();
    };

    $scope.clearAlerts = function(){
        $scope.info = false;
        $scope.success = false;
        $scope.danger = false;
    };

    $scope.saveData = function(){

        $scope.clearAlerts();

        var id = $scope.form.id;
        if (!id.match(/^\d+$/)){
            $scope.danger = true;
            $scope.message = "La identificación debe ser un entero";

        } else if (typeof $scope.form.nombre === "undefined"  || typeof $scope.form.apellido === "undefined"){
            $scope.danger = true;
            $scope.message = "El nombre y apellido deben estar completos";

        } else {
            var data = {
            'id': $scope.form.id,
            'nombre': $scope.form.nombre,
            'apellido': $scope.form.apellido,
            'email': $scope.form.email
            }

            console.log(data);

            var xhr = new XMLHttpRequest();
            var url = "/registrar";
            xhr.open("POST", url, true);
            xhr.setRequestHeader("Content-type", "application/json")
            xhr.onreadystatechange = function () {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    var json = JSON.parse(xhr.responseText);

                    setTimeout(function () {
                        $scope.$apply(function(){

                            console.log(json);

                           if (json.status == 200){
                                $scope.success = true;
                                $scope.message = "El usuario fue registrado satisfactoriamente";

                                $scope.twostep = true;
                                $scope.tree_step = true;

                            } else if (json.status == 403){
                                $scope.info = true;
                                $scope.message = "El usuario ya se encuentra registrado";
                            }

                        });
                    }, 2000);
                } else {
                    console.log('Oops');
                }
            }
            var data = JSON.stringify(data);
            xhr.send(data);

        }

    };

    $scope.saveRequest = function(){

        $scope.clearAlerts();

        var nit = $scope.form.nit;


        if (!nit.match(/^\d+$/)){
            $scope.danger = true;
            $scope.message = "El NIT debe ser un entero";

        } else if (typeof $scope.form.salario === "undefined"  || !typeof $scope.form.salario.match(/^\d+$/)) {

            var salario = $scope.form.salario;

            $scope.danger = true;
            $scope.message = "El salario debe ser entero y/o estar completo el campo";

        }
       else {
            var data = {
            'id': $scope.form.id,
            'nit': $scope.form.nit,
            'salario': $scope.form.salario
            }

            console.log(data);

            var xhr = new XMLHttpRequest();
            var url = "/solicitar";
            xhr.open("POST", url, true);
            xhr.setRequestHeader("Content-type", "application/json")
            xhr.onreadystatechange = function () {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    var json = JSON.parse(xhr.responseText);

                    setTimeout(function () {
                        $scope.$apply(function(){

                            console.log(json);

                           if (json.status == 200){
                                $scope.success = true;

                                if(json.status == 'RECHAZADO'){
                                    $scope.warning = true;
                                    $scope.message = "En el momento ud no cumple con las condiciones";
                                    $scope.tree_step = false;
                                } else {
                                    $scope.success = true;
                                    $scope.message = "Señor usuario " + $scope.form.nombre + " su credito fue aprobado por " + json.valor_aprobado;
                                    $scope.tree_step = false;
                                }
                        }});
                    }, 2000);
                } else {
                    console.log('Oops');
                }
            }
            var data = JSON.stringify(data);
            xhr.send(data);

        }

    };


});

todoCtrl.$inject = ['$window','$scope'];
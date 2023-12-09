function Identity(name, exe_fn) {
    this.name = name;
    this.exe = function () {
        exe_fn()
    }
}


let Wolf = new Identity('狼人');
let Witch = new Identity('女巫');
let Villager = new Identity('村民');
let Prophet = new Identity('预言家');


// export
identities = [
    Wolf,
    Witch,
    Villager,
    Prophet,
];

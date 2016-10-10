var express = require('express');

var app = express();

var model = {
    '1': { text: 'Does it have two legs?' },
    '2': { text: 'Does it have feathers?' },
    '3': { text: 'Does it have hoof?' },
    '4': { text: 'Is it quacking?' },
    '5': { text: 'Is it a man?' },
    '6': { text: 'Is it a cloven-hoofed?' },
    '7': { text: 'Is it pulling in claws?' },
    '8': 'A Duck',
    '9': 'A Chicken',
    '10': 'A Human',
    '11': 'A Monkey',
    '12': 'A Cow',
    '13': { text: 'Does it have horn?' },
    '14': 'A Cat',
    '15': 'A Dog',
    '26': 'A Rhinoceros',
    '27': 'A Horse'
};

app.set('view engine', 'jade');
app.use(express.static('static'));

var bodyParser = require('body-parser');
app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies


app.get('/', function(req, res) {
    res.redirect('/q/1')
})

app.get('/q/:question_id', function(req, res) {
    var id = +req.params.question_id;
    var question = model[id];

    if(typeof question == 'object') { // ask question
        res.render('index', {
            question: question.text,
            go_yes: '/q/' + (id * 2),
            go_no: '/q/' + (id * 2 + 1),
        })
    } else { // try to guess
        res.render('index', {
            question: 'Is it ' + question + '?',
            go_yes: '/hurray',
            go_no: '/wrong_guess/' + id,
        })
    }
});

app.get('/hurray', function(req, res) {
    res.send('Congratulations! You are winner!!! <a href="/q/1">New game!</a>')
})

app.get('/wrong_guess/:question_id', function(req, res) {
    var id = +req.params.question_id;
    res.render('add_question', {
        animal: model[id],
    })
})

app.post('/wrong_guess/:question_id', function(req, res) {
    var id = +req.params.question_id;
    var old_animal = model[id];
    var new_animal = req.body.new_animal;

    if(req.body.right_answer == 'yes') {
        model[id * 2] = old_animal;
        model[id * 2 + 1] = new_animal;
    } else  {
        model[id * 2] = new_animal;
        model[id * 2 + 1] = old_animal;
    };

    model[id] = {
        text: req.body.new_question,
    }
    console.log(model);
    res.send('Thank you for the hint! <a href="/q/1">New game!</a>')
})


app.listen(3000, function() {
    console.log('Listening on port 3000');
})

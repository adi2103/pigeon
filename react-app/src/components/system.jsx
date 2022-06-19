import React from 'react';
import ring from '../ring.jpg';
import axios from 'axios'
import '../App.css';

export default class System extends React.Component {
    handleReset = () => {
        window.location.reload();
    };

    render() {
        function onAnimationEnd() {
            var letter = document.getElementById('letter');
            var envelope = document.getElementById('envelope');
            var envelopeTop = document.getElementById('top');
            var pigeon = document.getElementById('pigeon');
            var cover = document.getElementById('cover');
            var phoneNumber = document.getElementById('phone-number');
            var message = document.getElementById('message');
            var callSid = document.getElementById('call-sid');
            var ring = document.getElementById('ring');

            letter.classList.remove("submit1");
            letter.classList.remove("submit2");
            letter.style.display = "none";
            envelope.style.backgroundColor = "#ffffff";
            envelope.style.zIndex = -10;
            envelopeTop.classList.remove("open");
            envelopeTop.classList.add("close");
            pigeon.classList.add("deliver");
            cover.classList.add("animate");

            pigeon.addEventListener("animationend", function () {
                const data = {
                    phone_number: phoneNumber.value,
                    message: message.value
                }

                axios.post('https://pigeon-ufonia.herokuapp.com/calls', data)
                    .then(response => {
                        callSid.innerText = response.data.call_sid
                        ring.src = "images/ring.gif";
                    })
                    .catch(error => {
                        callSid.innerText = error.message
                        callSid.backgroundColor = "red"
                    });
            })

            letter.removeEventListener('animationend', onAnimationEnd);
        }
        function handleSubmit(e) {
            e.preventDefault()
            var letter = document.getElementById('letter');
            var bottomRight = document.getElementById('bottom-right');
            var left = document.getElementById('left');
            var submit = document.getElementById('submit');
            var phoneNumber = document.getElementById('phone-number');

            submit.style.visibility = "hidden";
            phoneNumber.style.visibility = "hidden"
            letter.classList.add("submit1");
            letter.addEventListener("animationend", function () {
                letter.classList.remove('initial');
                left.style.zIndex = 5;
                bottomRight.style.zIndex = 5;
                letter.style.zIndex = 3;
                letter.classList.remove("submit1");
                letter.classList.add("submit2");
                letter.addEventListener("animationend", onAnimationEnd)
            })
        }
        return (
            <div className="envelope" id="envelope">
                <div id="cover">
                    <div className="cover top open" id="top"></div>
                    <div className="cover bottom right" id="bottom-right"></div>
                    <div className="cover left" id="left"></div>
                </div>
                <div className="letter initial" id="letter">
                    Message
                    _________________
                    _________________
                    _________________
                    <form id="form" onSubmit={handleSubmit}>
                        <textarea id="message" type="text" rows="3" cols="20" wrap="soft" required={true} />
                        <input id="phone-number" className="number" type="text" maxLength={15} placeholder="(+xx) xxxxxxxxxx" required={true} />
                        <input id="submit" className="submitButton" type="submit" value="Send" />
                    </form>
                </div>
                <span id="call-sid" className="callSid">Call Sid: ??????????????????</span>
                <input type="submit" className="reset" value="Reset" onClick={this.handleReset} />
                <div id="pigeon" className="pigeon" />
                <img src={ring} id="ring" className="ring" alt="ring"/>
            </div>
        )
    }
}
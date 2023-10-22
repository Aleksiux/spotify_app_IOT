document.getElementById("device").addEventListener("change", function () {
        var selectedOption = this.options[this.selectedIndex].value;
        document.getElementById("selected_device").value = selectedOption;
    });
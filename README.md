# Python implementation of BCOSFIRE  


<p align="center">
  <a href="./data/sample_0.png">
    <img src="./data/sample_0.png" alt="Sample image" width="300" height="300" >
    <img src="./figures/sample_0_out.png" alt="Sample image output" width="300" height="300">
  </a>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <!-- <li><a href="#prerequisites">Prerequisites</a></li> -->
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <!-- <li><a href="#acknowledgements">Acknowledgements</a></li> -->
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This is a Python implementation of the B-COSFIRE algorithm, which was originally [implemented](https://de.mathworks.com/matlabcentral/fileexchange/49172-trainable-cosfire-filters-for-curvilinear-structure-delineation-in-images) in MATLAB by Nicola Strisciuglio et. al. Please find the B-COSFIRE paper [here](http://dx.doi.org/10.1016/j.media.2014.08.002) (2015).

The B-COSFIRE filter aims to segment elongated patterns in images such as blood vessels in retinal images. It is based on an existing filter, so-called Combination Of Shifted FIlter Responses (COSFIRE). While the COSFIRE filters are used to detect bifurcations in the retinal images, the B-COSFIRE filters (as B stands for bar) are used to detect bar-like structures (e.g. vessels) in the images. Please check [the COSFIRE paper](https://www.sciencedirect.com/science/article/abs/pii/S0167865512003625) (2013) to understand the basics of the algorithm. 

The core of the B-COSFIRE algorithm relies on the [Difference-of-Gaussians](https://en.wikipedia.org/wiki/Difference_of_Gaussians) (DoG) filters which are used for detecting lines and edges. Since the vessels in the retinal images vary in orientation and thickness, it is a challenging task to define convenient filters for such a complexity. The B-COSFIRE algorithm comes up with a smart idea for this challenge:

1) The user provides a vessel-like prototype pattern, e.g., a bar.
2) The pattern is filtered with a DoG filter followed by a blur operation in order to reduce the noise.
3) The positions of the maximum points on the bar are marked by using a circle strategy.
4) A DoG filter is defined for each position.
5) The input image (e.g. retinal image) is filtered with the shifted DoG filters, and this results in the DoG responses.
6) The weighted geometric mean of the DoG responses give the output of the B-COSFIRE filter.  


### Built With
You need `python3` for this project. 

<!-- GETTING STARTED -->
## Getting Started
To get a local copy, you can follow the following steps.
### Installation
You can install the repository and required Python packages by following the steps below.

1. Clone the repo
  ```sh
  git clone https://github.com/Brains-for-hire/diabetic-retinopathy/tree/master/cosfire
  ```
2. Install required packages
  ```sh
  pip3 install -r requirements.txt
  ```
<!-- USAGE EXAMPLES -->
## Usage
To run the BCOSFIRE algorithm on the sample image `./data/sample_0.png`, you can run the following command in the terminal.
  ```sh
  python3 BCOSFIRE.py ./data/sample_0.png
  ```

<!-- ROADMAP -->
## Roadmap
See the [open issues](./issues) for a list of known issues.

<!-- CONTRIBUTING -->
## Contributing

Any contributions are **greatly appreciated**.

Contributions might include anything which make the code being more efficient and yielding better results. 

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the *BSD-3-Clause License*. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Project Link: [Brains for hire UG](https://brainsforhire.eu/)

import torch
import torch.nn as nn


class ResnetBlock(nn.Module):
    def __init__(self, in_channels):
        super(ResnetBlock, self).__init__()
        self.conv_block = nn.Sequential(
            nn.ReflectionPad2d(1),
            nn.Conv2d(in_channels, in_channels, kernel_size=3, stride=1),
            nn.InstanceNorm2d(in_channels),
            nn.ReLU(inplace=True),
            nn.ReflectionPad2d(1),
            nn.Conv2d(in_channels, in_channels, kernel_size=3, stride=1),
            nn.InstanceNorm2d(in_channels),
        )

    def forward(self, x):
        return x + self.conv_block(x)


class GeneratorA(nn.Module):
    def __init__(self, input_channels=3, output_channels=3, num_residual_blocks=9):
        super(GeneratorA, self).__init__()

        # Initial Convolution Layer
        self.model = nn.Sequential(
            nn.ReflectionPad2d(3),
            nn.Conv2d(input_channels, 64, kernel_size=7, stride=1),
            nn.InstanceNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.InstanceNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1),
            nn.InstanceNorm2d(256),
            nn.ReLU(inplace=True),
        )

        # Residual Blocks
        for _ in range(num_residual_blocks):
            self.model.add_module("resnet_block", ResnetBlock(256))

        # Upsampling layers
        self.model.add_module("deconv1",
                              nn.ConvTranspose2d(256, 128, kernel_size=3, stride=2, padding=1, output_padding=1))
        self.model.add_module("inorm1", nn.InstanceNorm2d(128))
        self.model.add_module("relu1", nn.ReLU(inplace=True))
        self.model.add_module("deconv2",
                              nn.ConvTranspose2d(128, 64, kernel_size=3, stride=2, padding=1, output_padding=1))
        self.model.add_module("inorm2", nn.InstanceNorm2d(64))
        self.model.add_module("relu2", nn.ReLU(inplace=True))
        self.model.add_module("reflection_pad", nn.ReflectionPad2d(3))
        self.model.add_module("final_conv", nn.Conv2d(64, output_channels, kernel_size=7, stride=1))
        self.model.add_module("tanh", nn.Tanh())

    def forward(self, x):
        return self.model(x)


class GeneratorB(nn.Module):
    def __init__(self, input_channels=3, output_channels=3, num_residual_blocks=9):
        super(GeneratorB, self).__init__()

        # Initial Convolution Layer
        self.model = nn.Sequential(
            nn.ReflectionPad2d(3),
            nn.Conv2d(input_channels, 64, kernel_size=7, stride=1),
            nn.InstanceNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.InstanceNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1),
            nn.InstanceNorm2d(256),
            nn.ReLU(inplace=True),
        )

        # Residual Blocks
        for i in range(num_residual_blocks):
            self.model.add_module(f"resnet_block_{i}", ResnetBlock(256))

        # Upsampling layers
        self.model.add_module("deconv1",
                              nn.ConvTranspose2d(256, 128, kernel_size=3, stride=2, padding=1, output_padding=1))
        self.model.add_module("inorm1", nn.InstanceNorm2d(128))
        self.model.add_module("relu1", nn.ReLU(inplace=True))
        self.model.add_module("deconv2",
                              nn.ConvTranspose2d(128, 64, kernel_size=3, stride=2, padding=1, output_padding=1))
        self.model.add_module("inorm2", nn.InstanceNorm2d(64))
        self.model.add_module("relu2", nn.ReLU(inplace=True))
        self.model.add_module("reflection_pad", nn.ReflectionPad2d(3))
        self.model.add_module("final_conv", nn.Conv2d(64, output_channels, kernel_size=7, stride=1))
        self.model.add_module("tanh", nn.Tanh())

    def forward(self, x):
        return self.model(x)

class Generator(nn.Module):
    def __init__(self, generator_type='A', input_channels=3, output_channels=3, num_residual_blocks=9):
        super(Generator, self).__init__()

        if generator_type == 'A':
            self.model = GeneratorA(input_channels, output_channels, num_residual_blocks)
        elif generator_type == 'B':
            self.model = GeneratorB(input_channels, output_channels, num_residual_blocks)
        else:
            raise ValueError("Invalid generator type. Choose 'A' or 'B'.")

    def forward(self, x):
        return self.model(x)


def load_model(checkpoint_path, generator_type):
    model = Generator(generator_type)  # Instantiate based on the generator type
    try:
        checkpoint = torch.load(checkpoint_path)  # Load the checkpoint
        print("Checkpoint keys:", checkpoint.keys())  # Print available keys in the checkpoint

        # Load state dict with strict=False to allow flexibility in loading
        model.load_state_dict(checkpoint, strict=False)
        model.eval()  # Set to evaluation mode
        print("Model loaded successfully")

    except Exception as e:
        print(f"Error loading model: {e}")

    return model  # Return the loaded model
